var app = angular.module('home-controllers', []);

app.controller('InfomainController', function () {
    this.mInfo = infoContent;
});

app.controller('FlavormainController', function () {
    this.mFlavor = flavorContent;

});

app.controller('VendormainController', function () {
    this.mVendor = [
        {
            logo: "assets/images/logo-telkom-corpu.png"
        },
        {
            logo: "assets/images/dds-logo.png"
        },
        {
            logo: "assets/images/OpenStack-Logo.png"
        }
    ];
});

var infoContent = [
    {
        image: "assets/images/cloud-computing.png",
        title: "Layanan Cloud Cepat dan Handal",
        description: "Dengan penggunaan layanan yang berbasis OpenStack dan layanan support yang selalu tersedia."
    },
    {
        image: "assets/images/list.png",
        title: "Mendukung Semua yang Dibutuhkan",
        description: "Layanan kami mendukung semua fitur dan kebutuhan yang anda perlukan untuk cloud anda."
    }
];

var flavorContent = [
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
