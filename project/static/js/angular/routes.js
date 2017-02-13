angular.module('CloudDDS').config(function($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'template/index.html'
        })
        .when('/layanan', {
            templateUrl: 'template/layanan.html'
        })
        .when('/bantuan', {
            templateUrl: 'template/bantuan.html'
        })
        .otherwise({
            redirectTo: '/'
        });

    $locationProvider.html5Mode(true);
});