const assert = require('node:assert/strict')
const { test } = require('node:test')
const fs = require('node:fs')
const path = require('node:path')
const compiler = require('vue-template-compiler')

// Exercise component options without mounting a browser or starting the app.
function parse(relativePath) {
  return compiler.parseComponent(fs.readFileSync(path.join(__dirname, '..', relativePath), 'utf8'))
}

function loadComponent(relativePath) {
  const script = parse(relativePath).script.content
    .replace(/^import .+$/gm, '')
    .replace('export default', 'return')
  return new Function('GeneralServices', 'DraftPoolSelection', script)(class {}, {})
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

const selector = loadComponent('components/draftPool/DraftPoolSelection.vue')
const positions = [{ id: 1, name: 'Goalkeepers' }, { id: 2, name: 'Attackers' }]
const players = [
  { id: 'gk-1', name: 'Keeper', position_id: 1, overall: 85 },
  { id: 'st-1', name: 'Striker', position_id: 2, overall: 90, locked: true, participant_id: 7, team_participant: 'Reds' },
  { id: 'st-2', name: 'Forward', position_id: 2, overall: 80 },
]

test('templates compile', () => {
  for (const file of ['components/draftPool/DraftPoolSelection.vue', 'components/dialogs/draftPool/index.vue']) {
    assert.deepEqual(compiler.compile(parse(file).template.content).errors, [], file)
  }
})

test('groups players by position', () => {
  const { context } = instance(selector, { value: [], players, positions })
  assert.deepEqual(context.groups.map(group => group.players.map(player => player.id)), [['gk-1'], ['st-1', 'st-2']])
})

test('deselecting a position keeps locked players selected', () => {
  const { context, emitted } = instance(selector, { value: ['gk-1', 'st-1', 'st-2'], players, positions })
  context.togglePosition(context.groups[1])
  assert.deepEqual(emitted, [['input', ['gk-1', 'st-1']]])
})

test('selecting a position adds every player once', () => {
  const { context, emitted } = instance(selector, { value: ['st-1'], players, positions })
  context.togglePosition(context.groups[1])
  assert.deepEqual(emitted, [['input', ['st-1', 'st-2']]])
})

test('locked players cannot be toggled', () => {
  const { context, emitted } = instance(selector, { value: ['st-1'], players, positions })
  context.togglePlayer(players[1], false)
  assert.deepEqual(emitted, [])
  assert.equal(context.lockedReason(players[1]), 'Assigned to Reds')
  assert.equal(context.lockedReason({ ...players[2], locked: true }), 'Open auction')
})

test('search filters players by name', () => {
  const { context } = instance(selector, { value: [], players, positions })
  context.search = 'forw'
  assert.deepEqual(context.filteredPlayers(context.groups[1]).map(player => player.id), ['st-2'])
})
