var app = angular.module('AppControllers', []);

/* Main Controller */
app.controller('InfomainController', function () {
    this.mInfo = [
        {
            image: "../static/img/cloud-computing.png",
            title: "Layanan Cloud Cepat dan Handal",
            description: "Dengan penggunaan layanan yang berbasis OpenStack dan layanan support yang selalu tersedia."
        },
        {
            image: "../static/img/list.png",
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

/* Layanan Controllers */
app.controller('FlavorlayananController', function () {
    this.tab = 0;

    this.lFlavor = layananFlavor;

    this.getTab = this.tab;
});

app.controller('AppslayananController', function () {
    this.lApps = apps;
});

var layananFlavor = [
    {
        type: "S",
        vcpu: 1,
        ram: 1,
        swap: 1,
        disk: 20,
        public_ip: 1,
        price: 100
    },
    {
        type: "M",
        vcpu: 1,
        ram: 2,
        swap: 1,
        disk: 40,
        public_ip: 1,
        price: 200
    },
    {
        type: "L",
        vcpu: 2,
        ram: 2,
        swap: 2,
        disk: 60,
        public_ip: 1,
        price: 300
    },
    {
        type: "XL",
        vcpu: 2,
        ram: 4,
        swap: 2,
        disk: 80,
        public_ip: 1,
        price: 400
    }
];

var apps = [
    {
        nama: 'Django'
    },
    {
        nama: 'Docker'
    },
    {
        nama: 'Ghost'
    },
    {
        nama: 'GitLab'
    },
    {
        nama: 'Horizon'
    },
    {
        nama: 'Lamp'
    },
    {
        nama: 'Lemp'
    },
    {
        nama: 'MEAN'
    },
    {
        nama: 'MongoDB'
    },
    {
        nama: 'Node.Js'
    },
    {
        nama: 'ownCloud'
    },
    {
        nama: 'Redis'
    },
    {
        nama: 'Ruby on Rails'
    },
    {
        nama: 'WordPress'
    }
];

/* Bantuan Controllers */
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