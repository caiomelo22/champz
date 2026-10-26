const assert = require('node:assert/strict')
const { test } = require('node:test')
const fs = require('node:fs')
const path = require('node:path')

const script = fs.readFileSync(path.join(__dirname, '../pages/championship/_id/draft/index.js'), 'utf8')
  .replace(/^import (\w+) .+$/gm, 'const $1 = class {}')
  .replace('export default', 'return')
// Evaluate only the trusted, local component options without starting Nuxt.
// eslint-disable-next-line no-new-func
const draft = new Function(script)()
const previousAuction = {
  id: 7,
  player_id: 'hakimi',
  player_name: 'Achraf Hakimi',
  status: 'open',
  leading_participant_id: 2,
  leading_bid: 26,
  is_current_user_leader: true,
}

function setup(overrides = {}) {
  const requests = []
  const notifications = []
  const context = {
    ...draft.data(),
    $route: { params: { id: 1 } },
    accessRole: 'participant',
    myParticipantId: 2,
    participants: [{ id: 2, budget: 74 }, { id: 3, budget: null }],
    positions: [{ id: 4 }],
    auctionsByPlayer: { hakimi: { ...previousAuction } },
    $set: (object, key, value) => { object[key] = value },
    $toast: {
      info: message => notifications.push(['info', message]),
      error: message => notifications.push(['error', message]),
      success: message => notifications.push(['success', message]),
    },
    ...overrides,
  }
  Object.entries(draft.methods).forEach(([name, method]) => { context[name] = method.bind(context) })
  Object.entries(draft.computed).forEach(([name, getter]) => {
    Object.defineProperty(context, name, { get: () => getter.call(context) })
  })
  let nextAuction = { ...previousAuction, leading_participant_id: 3, leading_bid: 27, is_current_user_leader: false }
  let balances = [{ id: 2, budget: 100 }, { id: 3, budget: null }]
  let failBalance = false
  context.$axios = {
    get: (url) => {
      requests.push(url)
      if (url.endsWith('/auction/list')) { return Promise.resolve({ data: [nextAuction] }) }
      if (url.endsWith('/participant/list')) {
        assert.equal(context.participantsLoading, false, 'Background balance refresh must not hide participants')
        if (failBalance) { return Promise.reject(new Error('offline')) }
        return Promise.resolve({ data: balances })
      }
      if (url.includes('/player/list')) { return Promise.resolve({ data: [] }) }
      throw new Error(`Unexpected request: ${url}`)
    },
  }
  return {
    context,
    requests,
    notifications,
    setAuction: auction => { nextAuction = auction },
    setBalances: participants => { balances = participants },
    setBalanceFailure: failing => { failBalance = failing },
  }
}

test('outbid polling restores available budget and participant balance without a page refresh', async () => {
  const { context, requests, notifications } = setup()
  await context.get_auctions()
  assert.equal(context.availableBudget, 100)
  assert.equal(context.participants[0].budget, 100)
  assert.equal(context.participants[1].budget, null)
  assert.deepEqual(notifications, [['info', 'You were outbid for Achraf Hakimi.']])
  assert.deepEqual(requests, ['championship/1/auction/list', 'championship/1/participant/list'])
})

test('remote cancellation refreshes refunded balance without an outbid notification', async () => {
  const { context, setAuction, notifications } = setup()
  setAuction({ ...previousAuction, status: 'cancelled' })
  await context.get_auctions()
  assert.equal(context.availableBudget, 100)
  assert.deepEqual(notifications, [])
})

test('a higher bid by the same leader also updates available budget', async () => {
  const { context, setAuction, setBalances } = setup()
  setAuction({ ...previousAuction, leading_bid: 30 })
  setBalances([{ id: 2, budget: 70 }, { id: 3, budget: null }])
  await context.get_auctions()
  assert.equal(context.availableBudget, 70)
})

test('closing refreshes balances even when no position is selected', async () => {
  const { context, setAuction } = setup({ positions: [] })
  setAuction({ ...previousAuction, status: 'closed' })
  await context.get_auctions()
  assert.equal(context.availableBudget, 100)
})

test('unchanged auctions do not repeatedly request participant balances', async () => {
  const { context, requests, setAuction } = setup()
  setAuction({ ...previousAuction })
  await context.get_auctions()
  assert.deepEqual(requests, ['championship/1/auction/list'])
})

test('initial auction snapshot reconciles a bid received after the first participant load', async () => {
  const { context } = setup({ auctionsByPlayer: {} })
  await context.get_auctions()
  assert.equal(context.availableBudget, 100)
})

test('failed balance refresh retries on next poll even if the auction no longer changes', async () => {
  const { context, requests, setBalanceFailure } = setup()
  setBalanceFailure(true)
  await context.get_auctions()
  assert.equal(context.availableBudget, 74)
  assert.equal(context.auctionPolling, false)
  setBalanceFailure(false)
  await context.get_auctions()
  assert.equal(context.availableBudget, 100)
  assert.equal(requests.filter(url => url.endsWith('/participant/list')).length, 2)
})

test('a locally submitted manager bid refreshes the refunded leader as well as the new leader', async () => {
  const { context, requests, setBalances } = setup({
    accessRole: 'owner',
    participants: [{ id: 2, budget: 74 }, { id: 3, budget: 100 }],
  })
  setBalances([{ id: 2, budget: 100 }, { id: 3, budget: 73 }])
  await context.bid_saved({
    auction: { ...previousAuction, leading_participant_id: 3, leading_bid: 27, is_current_user_leader: false },
    available_budget: 73,
  })
  assert.equal(context.participants[0].budget, 100)
  assert.equal(context.participants[1].budget, 73)
  assert.equal(context.placeBidDialog, false)
  assert.deepEqual(requests, ['championship/1/participant/list'])
})

test('a failed post-bid balance refresh is retried automatically by polling', async () => {
  const { context, setBalanceFailure } = setup()
  setBalanceFailure(true)
  await context.bid_saved({
    auction: { ...previousAuction, leading_participant_id: 3, leading_bid: 27, is_current_user_leader: false },
    available_budget: 73,
  })
  assert.equal(context.participantBudgetsDirty, true)
  assert.equal(context.participants[0].budget, 74)
  setBalanceFailure(false)
  await context.get_auctions()
  assert.equal(context.availableBudget, 100)
  assert.equal(context.participantBudgetsDirty, false)
})