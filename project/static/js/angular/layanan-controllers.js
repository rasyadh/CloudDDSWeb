(function () {
    var app = angular.module('layanan-controllers', []);

    app.controller('FlavorlayananController', function () {
        this.tab = 0;

        this.lFlavor = layananFlavor;

        this.getTab = this.tab;

        /* this.setFlav = function(flav){
            this.flav = flav;
        };
    
        this.getFlav = function(){
            return this.flav;
        }; */
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

})();