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

app.controller('FlavormainController', function ($scope) {
    this.mFlavor = listFlavor;
    
    $scope.select = function(index){
        $scope.data = index;
    }

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
    this.lFlavor = listFlavor;

    $scope.selectedIndex = 0;
    
    $scope.select = function(index){
        $scope.selectedIndex = index;
    }
        
});

var listFlavor = [
    {
        type: "Small",
        color: "red",
        vcpu: 1,
        ram: 1,
        disk: 20,
        detail: "Cocok digunakan untuk membuat hosting"
    },
    {
        type: "Medium",
        color: "yellow",
        vcpu: 1,
        ram: 2,
        disk: 40,
        detail: "Cocok digunakan untuk development aplikasi web dan lainnya"
    },
    {
        type: "Large",
        color: "green",
        vcpu: 2,
        ram: 2,
        disk: 60,
        detail: "Cocok digunakan untuk development dengan menggunakan container"
    },
    {
        type: "Custom",
        color: "blue",
        vcpu: "Custom",
        ram: "Custom",
        disk: "Custom",
        detail: "Cocok digunakan untuk kebutuhan dengan spesifikasi yang tinggi"
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
app.controller('InfobantuanController', function ($scope, $http) {
    this.bInfo = [
        {

            title: "Apakah itu VM (Virtual Machine) ?",
            content: "Virtual Machine adalah implementasi perangkat lunak dari sebuah mesin komputer yang dapat menjalankan program sama seperti layaknya sebuah komputer asli."
        },
        {
            title: "Mekanisme request VM ?",
            steps: [
                {
                    desc: "Login"
                },
                {
                    desc: "Pilih Create VM"
                },
                {
                    desc: "Pilih sesuai kebutuhan"
                },
                {
                    desc: "Verifikasi lewat email"
                },
                {
                    desc: "VM Aktif"
                }
            ]
        },
        {
            title: "Cara Mengakses VM ?",
            steps: [
                {
                    desc: "Login"
                },
                {
                    desc: "Buka VM lewat IP"
                },
                {
                    desc: "Login"
                }
            ]
        },
        {
            title: "Cara Memanajemen VM ?",
            steps: [
                {
                    desc: "Login"
                },
                {
                    desc: "Pilih Manage VM"
                },
                {
                    desc: "Manajemen VM sesuai kebutuhan"
                }
            ]
        },
        {
            title: "Cara melakukan upgrade VM (Scale Up) ?",
            steps: [
                {
                    desc: "Login"
                },
                {
                    desc: "Pilih Manage VM"
                },
                {
                    desc: "Pilih Scale Up"
                },
                {
                    desc: "Masukkan spesifikasi request"
                },
                {
                    desc: "Email dan Telefon Konfirmasi"
                },
                {
                    desc: "VM ter-upgrade"
                }
            ]
        },
        {
            title: "Cara menghapus VM ?",
            steps: [
                {
                    desc: "Login"
                },
                {
                    desc: "Pilih Manage VM"
                },
                {
                    desc: "Pilih Delete VM"
                }
            ]
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