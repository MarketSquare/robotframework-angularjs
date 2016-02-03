# AngularJSLibrary - robotframework-angularjs
An AngularJS extension to Robotframework's Selenium2Library

## What is included

AngularJSLibrary provides keywords for finding elements by binding, model, and repeater. The library also provides a keyword for waiting on angular.

## Installation

To install **AngularJSLibrary**, run:

```
pip install robotframework-angularjs
```

Alternatively, to install from source:

```
python setup.py install
```

## Keyword Usage

The new locator strategies include

```
binding=
model=
repeater=
```

For example, you can look for an Angular ng-binding using

```
Get Text  binding={{greeting}}
```

or by using partial match

```
Get Text  binding=greet
```

or by simply using the binding {{…}} notation

```
Get Text  {{greeting}}
```

One can also find elements  by model

```
Input Text  model=aboutbox  Something else to write about
```

Finally there is the strategy of find by repeat. This takes the general form of repeater=some ngRepeat directive@row[n]@column={{ngBinding}}. Here we specify the directive as well as the row, an zero-based index, and the column, an ngBinding. Using this full format will return, if exists the element matching the directive, row and column binding.  One does not need to specify the row and column but can specify either both, one or the other or neither. In such cases the locator may return  list  of elements or even a list of list of elements. Also the ordering of row and column does not matter; using repeater=baz in days@row[0]@column=b is the same as repeater=baz in days@column=b @row[0].

## Getting Help

If you need help with AngularJSLibrary, Selenium2Library, or Robot Framework usage, please post to the [user group for Robot Framework](https://groups.google.com/forum/#!forum/robotframework-users).

## References