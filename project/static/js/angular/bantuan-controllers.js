(function () {
    var app = angular.module('bantuan-controllers', []);

    app.controller('InfobantuanController', function () {
        this.bInfo = [
            {
                image: "static/img/question.png",
                title: "FAQ",
                description: "Frequently asked questions."
            },
            {
                image: "static/img/customer-service.png",
                title: "Customer Service",
                description: "Layanan customer service 24 jam."
            }
        ];
    });

})();