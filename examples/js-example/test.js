const _ = require('lodash');

test('lodash map works', () => {
  const result = _.map([1, 2, 3], x => x * 2);
  expect(result).toEqual([2, 4, 6]);
}); 