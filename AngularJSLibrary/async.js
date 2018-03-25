function AsyncCtrl($scope, $http, $timeout, $location) {
  $scope.slowHttpStatus = 'not started';
  $scope.slowFunctionStatus = 'not started';
  $scope.slowTimeoutStatus = 'not started';
  $scope.slowAngularTimeoutStatus = 'not started';
  $scope.slowAngularTimeoutCompleted = false;
  $scope.slowAngularTimeoutPromiseStatus = 'not started';
  $scope.slowAngularTimeoutPromiseCompleted = false;
  $scope.slowHttpPromiseStatus = 'not started';
  $scope.slowHttpPromiseCompleted = false;
  $scope.routingChangeStatus = 'not started';
  $scope.templateUrl = 'fastTemplateUrl';

  $scope.slowHttp = function() {
    $scope.slowHttpStatus = 'pending...';
    $http({method: 'GET', url: 'slowcall'}).success(function() {
      $scope.slowHttpStatus = 'done';
    });
  };

  $scope.slowFunction = function() {
    $scope.slowFunctionStatus = 'pending...';
    for (var i = 0, t = 0; i < 500000000; ++i) {
      t++;
    }
    $scope.slowFunctionStatus = 'done';
  };

  $scope.slowTimeout = function() {
    $scope.slowTimeoutStatus = 'pending...';
    window.setTimeout(function() {
      $scope.$apply(function() {
        $scope.slowTimeoutStatus = 'done';
      });
    }, 5000);
  };

  $scope.slowAngularTimeout = function() {
    $scope.slowAngularTimeoutStatus = 'pending...';
    $timeout(function() {
      $scope.slowAngularTimeoutStatus = 'done';
      $scope.slowAngularTimeoutCompleted = true;
    }, 4000);
  };

  $scope.slowAngularTimeoutHideButton = function() {
    $scope.slowAngularTimeoutCompleted = false;
  };

  $scope.slowAngularTimeoutPromise = function() {
    $scope.slowAngularTimeoutPromiseStatus = 'pending...';
    $timeout(function() {
      // intentionally empty
    }, 4000).then(function() {
      $scope.slowAngularTimeoutPromiseStatus = 'done';
      $scope.slowAngularTimeoutPromiseCompleted = true;
    });
  };

  $scope.slowAngularTimeoutPromiseHideButton = function() {
    $scope.slowAngularTimeoutPromiseCompleted = false;
  };

  $scope.slowHttpPromise = function() {
    $scope.slowHttpPromiseStatus = 'pending...';
    $http({method: 'GET', url: 'slowcall'}).success(function() {
      // intentionally empty
    }).then(function() {
      $scope.slowHttpPromiseStatus = 'done';
      $scope.slowHttpPromiseCompleted = true;
    });
  };

  $scope.slowHttpPromiseHideButton = function() {
    $scope.slowHttpPromiseCompleted = false;
  };

  $scope.routingChange = function() {
    $scope.routingChangeStatus = 'pending...';
    $location.url('slowloader');
  };

  $scope.changeTemplateUrl = function() {
    $scope.templateUrl = 'slowTemplateUrl';
  };
}

AsyncCtrl.$inject = ['$scope', '$http', '$timeout', '$location'];

angular.module('myApp.appVersion', []).
  value('version', '0.1-robotframework-angularjs-031618').
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);
