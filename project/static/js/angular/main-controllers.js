(function () {
    var app = angular.module("main-controllers", []);

    app.controller('InfomainController', function () {
        this.mInfo = [
            {
                image: "static/img/cloud-computing.png",
                title: "Layanan Cloud Cepat dan Handal",
                description: "Dengan penggunaan layanan yang berbasis OpenStack dan layanan support yang selalu tersedia."
            },
            {
                image: "static/img/list.png",
                title: "Mendukung Semua yang Dibutuhkan",
                description: "Layanan kami mendukung semua fitur dan kebutuhan yang anda perlukan untuk cloud anda."
            }
        ];
    });

    app.controller('FlavormainController', function () {
        this.mFlavor = [
            {
                type: "Small",
                color: "red",
                memori: 1,
                processor: 1,
                disk: 20
            },
            {
                type: "Medium",
                color: "yellow",
                memori: 2,
                processor: 1,
                disk: 40
            },
            {
                type: "Large",
                color: "green",
                memori: 2,
                processor: 2,
                disk: 60
            },
            {
                type: "Extra Large",
                color: "blue",
                memori: 4,
                processor: 2,
                disk: 80
            }
        ];
    });

    app.controller('VendormainController', function () {
        this.mVendor = [
            {
                /** using flask sintaxis for url */
                logo_vendor: "static/img/logo-telkom-corpu.png"
            },
            {
                logo_vendor: "static/img/dds-logo.png"
            },
            {
                logo_vendor: "static/img/OpenStack-Logo.png"
            },
        ];
    });

})();