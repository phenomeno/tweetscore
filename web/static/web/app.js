var app = angular.module('tweetscore', ['ngRoute', 'ui.bootstrap']).config(function($routeProvider) {
  $routeProvider.
  when('/', {
    templateUrl: '/static/web/partials/user.html',
    controller: 'MainController'
  }).
  otherwise({
    redirectTo: '/'
  });
});
