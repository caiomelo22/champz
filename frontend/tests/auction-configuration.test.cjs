const assert = require('node:assert/strict')
const { test } = require('node:test')
const fs = require('node:fs')
const path = require('node:path')
const compiler = require('vue-template-compiler')

// Exercise component options without mounting a browser or starting the app.
function loadComponent(relativePath) {
  const source = fs.readFileSync(path.join(__dirname, '..', relativePath), 'utf8')
  const script = compiler.parseComponent(source).script.content
    .replace(/^import .+$/gm, '')
    .replace('export default', 'return')
  return new Function('AuctionPlayerSelection', script)({})
}

function instance(component, props = {}) {
  const emitted = []
  const context = { ...props, $emit: (...args) => emitted.push(args) }
  if (component.data) { Object.assign(context, component.data.call(context)) }
  Object.entries(component.methods || {}).forEach(([name, method]) => { context[name] = method.bind(context) })
  Object.entries(component.computed || {}).forEach(([name, getter]) => {
    Object.defineProperty(context, name, { get: () => getter.call(context) })
  })
  return { context, emitted }
}

const selector = loadComponent('components/auctions/AuctionPlayerSelection.vue')
const dialog = loadComponent('components/dialogs/configureAuction/index.vue')
const groups = [
  { id: 1, name: 'CB', players: [
    { id: 1, name: 'Available', overall: 88 },
    { id: 2, name: 'Owned', overall: 87, participant_id: 5 },
    { id: 3, name: 'Open', overall: 86 },
    { id: 4, name: 'Cancelled', overall: 85 },
    { id: 5, name: 'Closed', overall: 84 },
  ] },
  { id: 2, name: 'GK', players: [{ id: 6, name: 'Keeper', overall: 90 }] },
]
const auctionsByPlayer = { 3: { status: 'open' }, 4: { status: 'cancelled' }, 5: { status: 'closed' } }

function makeDialog(props = {}) {
  return instance(dialog, { championshipId: 7, player: null, auction: null, positions: [], auctionsByPlayer: {}, ...props })
}

test('select all includes only eligible players and preserves other positions', () => {
  const { context, emitted } = instance(selector, { value: [6], groups, auctionsByPlayer })
  context.togglePosition(groups[0])
  assert.deepEqual(emitted.pop(), ['input', [6, 1, 4]])
  context.value = [6, 1, 4]
  assert.equal(context.allSelected(groups[0]), true)
  assert.equal(context.selectedCount(groups[0]), 2)
  context.togglePosition(groups[0])
  assert.deepEqual(emitted.pop(), ['input', [6]])
})

test('unavailable players expose a reason and cannot be selected', () => {
  const { context, emitted } = instance(selector, { value: [], groups, auctionsByPlayer })
  assert.equal(context.unavailableReason(groups[0].players[0]), '')
  for (const player of groups[0].players.filter(player => [2, 3, 5].includes(player.id))) {
    assert.ok(context.unavailableReason(player))
    context.togglePlayer(player, true)
  }
  assert.equal(emitted.length, 0)
  context.togglePlayer(groups[0].players[0], true)
  assert.deepEqual(emitted.pop(), ['input', [1]])
  context.value = [1]
  context.togglePlayer(groups[0].players[0], false)
  assert.deepEqual(emitted.pop(), ['input', []])
})

test('cancelled auctions can be selected unless the player already has an owner', () => {
  const { context, emitted } = instance(selector, { value: [], groups, auctionsByPlayer })
  const cancelledPlayer = groups[0].players.find(player => player.id === 4)
  assert.equal(context.unavailableReason(cancelledPlayer), '')
  context.togglePlayer(cancelledPlayer, true)
  assert.deepEqual(emitted.pop(), ['input', [4]])
  const assignedPlayer = { ...cancelledPlayer, participant_id: 5 }
  assert.match(context.unavailableReason(assignedPlayer), /owner/)
  context.togglePlayer(assignedPlayer, true)
  assert.equal(emitted.length, 0)
})

test('manual assignment is available only to managers for absent or cancelled auctions', () => {
  const script = fs.readFileSync(path.join(__dirname, '../pages/championship/_id/draft/index.js'), 'utf8')
    .replace(/^import (\w+) .+$/gm, 'const $1 = {}')
    .replace('export default', 'return')
  const draft = new Function(script)()
  const context = { isOwner: true, auction_for: id => auctionsByPlayer[id] || null }
  assert.equal(draft.methods.can_assign_manually.call(context, 1), true)
  assert.equal(draft.methods.can_assign_manually.call(context, 4), true)
  assert.equal(draft.methods.can_assign_manually.call(context, 3), false)
  assert.equal(draft.methods.can_assign_manually.call(context, 5), false)
  context.isOwner = false
  assert.equal(draft.methods.can_assign_manually.call(context, 1), false)
  assert.equal(draft.methods.can_assign_manually.call(context, 4), false)
})

test('cancelled banner disappears after manual assignment without hiding other auction states', () => {
  const source = fs.readFileSync(path.join(__dirname, '../pages/championship/_id/draft/index.vue'), 'utf8')
  const condition = source.match(/<div v-if="([^"]+)" class="auction-state"[^>]*>/)[1]
  const visible = new Function('player', 'auction_for', `return Boolean(${condition})`)
  const available = { id: 4, participant_id: null }
  const assigned = { id: 4, participant_id: 5 }
  assert.equal(visible(available, () => ({ status: 'cancelled' })), true)
  assert.equal(visible(assigned, () => ({ status: 'cancelled' })), false)
  assert.equal(visible(assigned, () => ({ status: 'closed' })), true)
  assert.equal(visible(available, () => ({ status: 'open' })), true)
  assert.equal(visible(available, () => null), false)
})

test('auction banner receives a style variant matching its status', () => {
  const source = fs.readFileSync(path.join(__dirname, '../pages/championship/_id/draft/index.vue'), 'utf8')
  const binding = source.match(/class="auction-state" :class="([^"]+)"/)[1]
  const variant = new Function('player', 'auction_for', `return ${binding}`)
  for (const status of ['open', 'cancelled', 'closed']) {
    assert.equal(variant({ id: 1 }, () => ({ status })), `auction-state--${status}`)
  }
})

test('polling removes selections that become unavailable', () => {
  const { context, emitted } = instance(selector, { value: [1, 3, 6], groups, auctionsByPlayer })
  selector.watch.eligibleIds.call(context)
  assert.deepEqual(emitted.pop(), ['input', [1, 6]])
})

test('bulk loads exactly the draft endpoint for each position', async () => {
  const { context } = makeDialog({ positions: groups.map(({ id, name }) => ({ id, name })) })
  const requests = []
  context.$axios = { get: (url) => {
    requests.push(url)
    return Promise.resolve({ data: groups[requests.length - 1].players })
  } }
  await context.loadPlayers()
  assert.deepEqual(requests, ['championship/7/player/list?position=1', 'championship/7/player/list?position=2'])
  assert.deepEqual(context.playerGroups, groups)
  assert.equal(context.loadingPlayers, false)
})

test('bulk sends one shared configuration with only eligible selected ids', async () => {
  const { context, emitted } = makeDialog({ auctionsByPlayer })
  context.playerGroups = groups
  context.selectedPlayerIds = [1, 2, 3, 4, 5, 6]
  context.minimumBid = 12
  const requests = []
  context.$axios = { post: (url, payload) => {
    requests.push({ url, payload })
    return Promise.resolve({ data: ['created'] })
  } }
  await context.save()
  assert.deepEqual(requests, [{ url: 'championship/7/auction/configure', payload: {
    player_ids: [1, 4, 6], minimum_bid: 12, deadline: new Date(context.deadline).toISOString(),
  } }])
  assert.deepEqual(emitted.pop(), ['saved', ['created']])
})

test('individual creation is preselected and does not load the position list', async () => {
  const { context } = makeDialog({ player: groups[0].players[0] })
  assert.equal(context.isBatch, false)
  let request
  context.$axios = { post: (url, payload) => {
    request = payload
    return Promise.resolve({ data: {} })
  } }
  dialog.created.call(context)
  await context.save()
  assert.deepEqual(request.player_ids, [1])
})

test('editing and restarting continue to patch the existing auction', async () => {
  for (const status of ['open', 'cancelled']) {
    const { context } = makeDialog({ auction: { id: 10, status, minimum_bid: 5, deadline: new Date(Date.now() + 86400000).toISOString() } })
    let request
    context.$axios = { patch: (url, payload) => {
      request = { url, payload }
      return Promise.resolve({ data: {} })
    } }
    assert.equal(context.isBatch, false)
    await context.save()
    assert.equal(request.url, 'championship/7/auction/10')
    assert.equal(request.payload.minimum_bid, 5)
    assert.equal('player_ids' in request.payload, false)
  }
})

test('validation rejects empty selections, invalid bids, and past deadlines without requests', async () => {
  const { context } = makeDialog()
  await context.save()
  assert.match(context.error, /players are required/)
  context.playerGroups = groups
  context.selectedPlayerIds = [1]
  context.minimumBid = -1
  await context.save()
  assert.match(context.error, /greater than zero/)
  context.minimumBid = 1
  context.deadline = '2000-01-01T10:00'
  await context.save()
  assert.match(context.error, /future/)
})

test('loading failure is recoverable and does not allow submission', async () => {
  const { context } = makeDialog({ positions: [{ id: 1 }] })
  context.$axios = { get: () => Promise.reject(new Error('offline')) }
  await context.loadPlayers()
  assert.ok(context.playersError)
  assert.equal(context.loadingPlayers, false)
  context.$axios.get = () => Promise.resolve({ data: [] })
  await context.loadPlayers()
  assert.equal(context.playersError, null)
})

test('modified Vue templates compile without errors', () => {
  for (const file of [
    'components/auctions/AuctionPlayerSelection.vue',
    'components/dialogs/configureAuction/index.vue',
    'pages/championship/_id/draft/index.vue',
    'pages/championship/_id/matches/index.vue',
  ]) {
    const source = fs.readFileSync(path.join(__dirname, '..', file), 'utf8')
    const template = compiler.parseComponent(source).template.content
    assert.deepEqual(compiler.compile(template).errors, [], file)
  }
})