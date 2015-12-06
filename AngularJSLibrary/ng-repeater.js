var rootSelector = null;

// Generate either by.repeater or by.exactRepeater
function byRepeaterInner(exact) {
  var name = 'by.' + (exact ? 'exactR' : 'r') + 'epeater';
  return function(repeatDescriptor) {
    return {
      getElements: function(using) {
        return findAllRepeaterRows(repeatDescriptor, exact, using);
      },
      //toString: function toString() {
      //  return name + '("' + repeatDescriptor + '")';
      //},
      row: function(index) {
        return {
          getElements: function(using) {
            return findRepeaterRows(repeatDescriptor, exact, index, using);
          },
          //toString: function toString() {
          //  return name + '(' + repeatDescriptor + '").row("' + index + '")"';
          //},
          column: function(binding) {
            return {
              getElements: function(using) {
                return findRepeaterElement(repeatDescriptor, exact, index, binding, using, rootSelector);
              }//,
              //toString: function toString() {
              //  return name + '("' + repeatDescriptor + '").row("' + index +
              //    '").column("' + binding + '")';
              //}
            };
          }
        };
      },
      column: function(binding) {
        return {
          getElements: function(using) {
            return findRepeaterColumn(repeatDescriptor, exact, binding, using, rootSelector);
          },
          //toString: function toString() {
          //  return name + '("' + repeatDescriptor + '").column("' +
          //    binding + '")';
          //},
          row: function(index) {
            return {
	      getElements: function (using) {
	        return findRepeaterElement(repeatDescriptor, exact, index, binding, using, rootSelector);
	      }//,
              //toString: function toString() {
              //  return name + '("' + repeatDescriptor + '").column("' +
              //    binding + '").row("' + index + '")';
              //}
            };
          }
        };
      }
    };
  };
}

/**
 * Find elements inside an ng-repeat.
 *
 * @view
 * <div ng-repeat="cat in pets">
 *   <span>{{cat.name}}</span>
 *   <span>{{cat.age}}</span>
 * </div>
 *
 * <div class="book-img" ng-repeat-start="book in library">
 *   <span>{{$index}}</span>
 * </div>
 * <div class="book-info" ng-repeat-end>
 *   <h4>{{book.name}}</h4>
 *   <p>{{book.blurb}}</p>
 * </div>
 *
 * @example
 * // Returns the DIV for the second cat.
 * var secondCat = element(by.repeater('cat in pets').row(1));
 *
 * // Returns the SPAN for the first cat's name.
 * var firstCatName = element(by.repeater('cat in pets').
 *     row(0).column('cat.name'));
 *
 * // Returns a promise that resolves to an array of WebElements from a column
 * var ages = element.all(
 *     by.repeater('cat in pets').column('cat.age'));
 *
 * // Returns a promise that resolves to an array of WebElements containing
 * // all top level elements repeated by the repeater. For 2 pets rows resolves
 * // to an array of 2 elements.
 * var rows = element.all(by.repeater('cat in pets'));
 *
 * // Returns a promise that resolves to an array of WebElements containing all
 * // the elements with a binding to the book's name.
 * var divs = element.all(by.repeater('book in library').column('book.name'));
 *
 * // Returns a promise that resolves to an array of WebElements containing
 * // the DIVs for the second book.
 * var bookInfo = element.all(by.repeater('book in library').row(1));
 *
 * // Returns the H4 for the first book's name.
 * var firstBookName = element(by.repeater('book in library').
 *     row(0).column('book.name'));
 *
 * // Returns a promise that resolves to an array of WebElements containing
 * // all top level elements repeated by the repeater. For 2 books divs
 * // resolves to an array of 4 elements.
 * var divs = element.all(by.repeater('book in library'));
 *
 * @param {string} repeatDescriptor
 * @return {{findElementsOverride: findElementsOverride, toString: Function|string}}
 */
repeater = byRepeaterInner(false);

/**
 * Find an element by exact repeater.
 *
 * @view
 * <li ng-repeat="person in peopleWithRedHair"></li>
 * <li ng-repeat="car in cars | orderBy:year"></li>
 *
 * @example
 * expect(element(by.exactRepeater('person in peopleWithRedHair')).isPresent())
 *     .toBe(true);
 * expect(element(by.exactRepeater('person in people')).isPresent()).toBe(false);
 * expect(element(by.exactRepeater('car in cars')).isPresent()).toBe(true);
 *
 * @param {string} repeatDescriptor
 * @return {{findElementsOverride: findElementsOverride, toString: Function|string}}
 */
exactRepeater = byRepeaterInner(true);

/*
var functions = {};

function wrapWithHelpers(fun) {
  var helpers = Array.prototype.slice.call(arguments, 1);
  if (!helpers.length) {
    return fun;
  }
  var FunClass = Function; // Get the linter to allow this eval
  return new FunClass(
      helpers.join(';') + String.fromCharCode(59) +
      '  return (' + fun.toString() + ').apply(this, arguments);');
}
*/

function repeaterMatch(ngRepeat, repeater, exact) {
  if (exact) {
    return ngRepeat.split(' track by ')[0].split(' as ')[0].split('|')[0].
        split('=')[0].trim() == repeater;
  } else {
    return ngRepeat.indexOf(repeater) != -1;
  }
}

function findRepeaterRows(repeater, exact, index, using) {
  using = using || document;

  var prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:'];
  var rows = [];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        rows.push(repeatElems[i]);
      }
    }
  }
  /* multiRows is an array of arrays, where each inner array contains
     one row of elements. */
  var multiRows = [];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat-start';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        var elem = repeatElems[i];
        var row = [];
        while (elem.nodeType != 8 ||
            !repeaterMatch(elem.nodeValue, repeater)) {
          if (elem.nodeType == 1) {
            row.push(elem);
          }
          elem = elem.nextSibling;
        }
        multiRows.push(row);
      }
    }
  }
  var row = rows[index] || [], multiRow = multiRows[index] || [];
  return [].concat(row, multiRow);
}
//functions.findRepeaterRows = wrapWithHelpers(findRepeaterRows, repeaterMatch); 

function findAllRepeaterRows(repeater, exact, using) {
  using = using || document;

  var rows = [];
  var prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:'];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        rows.push(repeatElems[i]);
      }
    }
  }
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat-start';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        var elem = repeatElems[i];
        while (elem.nodeType != 8 ||
            !repeaterMatch(elem.nodeValue, repeater)) {
          if (elem.nodeType == 1) {
            rows.push(elem);
          }
          elem = elem.nextSibling;
        }
      }
    }
  }
  return rows;
}
//functions.findAllRepeaterRows = wrapWithHelpers(findAllRepeaterRows, repeaterMatch);

function findRepeaterElement(repeater, exact, index, binding, using, rootSelector) {
  var matches = [];
  var root = document.querySelector(rootSelector || 'body');
  using = using || document;

  var rows = [];
  var prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:'];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        rows.push(repeatElems[i]);
      }
    }
  }
  /* multiRows is an array of arrays, where each inner array contains
     one row of elements. */
  var multiRows = [];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat-start';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        var elem = repeatElems[i];
        var row = [];
        while (elem.nodeType != 8 || (elem.nodeValue &&
            !repeaterMatch(elem.nodeValue, repeater))) {
          if (elem.nodeType == 1) {
            row.push(elem);
          }
          elem = elem.nextSibling;
        }
        multiRows.push(row);
      }
    }
  }
  var row = rows[index];
  var multiRow = multiRows[index];
  var bindings = [];
  if (row) {
    //if (angular.getTestability) {
    //  matches.push.apply(
    //      matches,
    //      angular.getTestability(root).findBindings(row, binding));
    //} else {
      if (row.className.indexOf('ng-binding') != -1) {
        bindings.push(row);
      }
      var childBindings = row.getElementsByClassName('ng-binding');
      for (var i = 0; i < childBindings.length; ++i) {
        bindings.push(childBindings[i]);
      }
    //}
  }
  if (multiRow) {
    for (var i = 0; i < multiRow.length; ++i) {
      var rowElem = multiRow[i];
      //if (angular.getTestability) {
      //  matches.push.apply(
      //      matches,
      //      angular.getTestability(root).findBindings(rowElem, binding));
      //} else {
        if (rowElem.className.indexOf('ng-binding') != -1) {
          bindings.push(rowElem);
        }
        var childBindings = rowElem.getElementsByClassName('ng-binding');
        for (var j = 0; j < childBindings.length; ++j) {
          bindings.push(childBindings[j]);
        }
      //}
    }
  }
  for (var i = 0; i < bindings.length; ++i) {
    var dataBinding = angular.element(bindings[i]).data('$binding');
    if (dataBinding) {
      var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
      if (bindingName.indexOf(binding) != -1) {
        matches.push(bindings[i]);
      }
    }
  }
  return matches;
}
//functions.findRepeaterElement = wrapWithHelpers(findRepeaterElement, repeaterMatch);

function findRepeaterColumn(repeater, exact, binding, using, rootSelector) {
  var matches = [];
  var root = document.querySelector(rootSelector || 'body');
  using = using || document;

  var rows = [];
  var prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:'];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        rows.push(repeatElems[i]);
      }
    }
  }
  /* multiRows is an array of arrays, where each inner array contains
     one row of elements. */
  var multiRows = [];
  for (var p = 0; p < prefixes.length; ++p) {
    var attr = prefixes[p] + 'repeat-start';
    var repeatElems = using.querySelectorAll('[' + attr + ']');
    attr = attr.replace(/\\/g, '');
    for (var i = 0; i < repeatElems.length; ++i) {
      if (repeaterMatch(repeatElems[i].getAttribute(attr), repeater, exact)) {
        var elem = repeatElems[i];
        var row = [];
        while (elem.nodeType != 8 || (elem.nodeValue &&
            !repeaterMatch(elem.nodeValue, repeater))) {
          if (elem.nodeType == 1) {
            row.push(elem);
          }
          elem = elem.nextSibling;
        }
        multiRows.push(row);
      }
    }
  }
  var bindings = [];
  for (var i = 0; i < rows.length; ++i) {
    //if (angular.getTestability) {
    //  matches.push.apply(
    //      matches,
    //      angular.getTestability(root).findBindings(rows[i], binding));
    //} else {
      if (rows[i].className.indexOf('ng-binding') != -1) {
        bindings.push(rows[i]);
      }
      var childBindings = rows[i].getElementsByClassName('ng-binding');
      for (var k = 0; k < childBindings.length; ++k) {
        bindings.push(childBindings[k]);
      }
    //}
  }
  for (var i = 0; i < multiRows.length; ++i) {
    for (var j = 0; j < multiRows[i].length; ++j) {
      //if (angular.getTestability) {
      //  matches.push.apply(
      //      matches,
      //      angular.getTestability(root).findBindings(multiRows[i][j], binding));
      //} else {
        var elem = multiRows[i][j];
        if (elem.className.indexOf('ng-binding') != -1) {
          bindings.push(elem);
        }
        var childBindings = elem.getElementsByClassName('ng-binding');
        for (var k = 0; k < childBindings.length; ++k) {
          bindings.push(childBindings[k]);
        }
      //}
    }
  }
  for (var j = 0; j < bindings.length; ++j) {
    var dataBinding = angular.element(bindings[j]).data('$binding');
    if (dataBinding) {
      var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding;
      if (bindingName.indexOf(binding) != -1) {
        matches.push(bindings[j]);
      }
    }
  }
  return matches;
}
//functions.findRepeaterColumn = wrapWithHelpers(findRepeaterColumn, repeaterMatch);
			     