var app = angular.module('AppControllers', []);

/* Main Controller */
app.controller('InfomainController', function () {
    this.mInfo = [
        {
            image: "../static/img/cloud-computing.png",
            title: "Freedom at VM Level"
        },
        {
            image: "../static/img/list.png",
            title: "Easy & On-Demand Activation"
        },
        {
            image: "../static/img/scaleup.png",
            title: "Scale Resource As You Grow"
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
            logo_vendor: "static/img/logo-telkom-indonesia.png"
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
app.controller('FlavorlayananController', function ($scope) {
    this.lFlavor = layananFlavor;

    $scope.selectedIndex = 0;
    
    $scope.select = function(index){
        $scope.selectedIndex = index;
    }
        
});

var layananFlavor = [
    {
        type: "S",
        vcpu: 1,
        ram: 1,
        swap: 1,
        disk: 20,
        public_ip: 1
    },
    {
        type: "M",
        vcpu: 1,
        ram: 2,
        swap: 1,
        disk: 40,
        public_ip: 1
    },
    {
        type: "L",
        vcpu: 2,
        ram: 2,
        swap: 2,
        disk: 60,
        public_ip: 1
    },
    {
        type: "XL",
        vcpu: 2,
        ram: 4,
        swap: 2,
        disk: 80,
        public_ip: 1
    },
    {
        type: "Custom",
        vcpu: "Custom",
        ram: "Custom",
        swap: "Custom",
        disk: "Custom",
        public_ip: 1
    }
];

app.controller('AppslayananController', function () {
    this.lApps = apps;
});


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
            title: "Apakah itu VM (Virtual Machine) ?",
            content: "Virtual Machine adalah implementasi perangkat lunak dari sebuah mesin komputer yang dapat menjalankan program sama seperti layaknya sebuah komputer asli."
        },
        {
            title: "Mekanisme request VM ?",
            content: "request VM"
        },
        {
            title: "Cara Mengakses VM ?",
            content: "Akses VM"
        },
        {
            title: "Cara Memanajemen VM ?",
            content: "manajemen VM"
        },
        {
            title: "Cara melakukan upgrade VM (Scale Up) ?",
            content: "scale up vm"
        },
        {
            title: "Cara menghapus VM ?",
            content: "delete VM"
        },
        {
            title: "Setting username dan password VM ?",
            content: "setting username dan password"
        },
        {
            title: "Migrasi data bagi developer ?",
            content: "migrasi"
        }
    ];
});