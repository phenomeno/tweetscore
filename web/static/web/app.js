var app = angular.module('tweetscore', ['ngRoute']).config(function($routeProvider) {
  $routeProvider.
  when('/', {
    templateUrl: '/static/web/partials/user.html',
    controller: 'MainController'
  }).
  otherwise({
    redirectTo: '/'
  });
});
