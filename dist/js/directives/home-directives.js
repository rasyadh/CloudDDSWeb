var app = angular.module('home-directives', []);

app.directive('mainFollowing', function () {
    return {
        restrict: 'E',
        templateUrl: 'template/views/main-following.html'
    };
});

app.directive('mainContent', function () {
    return {
        restrict: 'E',
        templateUrl: 'template/views/main-content.html'
    };
});

app.directive('mainVendor', function () {
    return {
        restrict: 'E',
        templateUrl: 'template/views/main-vendor.html'
    };
});

app.directive('mainFooter', function () {
    return {
        restrict: 'E',
        templateUrl: 'template/views/main-footer.html'
    };
});