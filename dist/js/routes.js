angular.module('CloudDDS').config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'template/views/main-content.html'
        })
        .when('/layanan', {
            templateUrl: 'template/views/layanan/layanan.html'
        })
        .when('/bantuan', {
            templateUrl: 'template/views/bantuan/bantuan.html'
        })
        .otherwise({
            redirectTo: '/'
        });
});