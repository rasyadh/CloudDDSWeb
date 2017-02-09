var app = angular.module('layanan-controllers', []);

app.controller('FlavorlayananController', function(){
    this.lFlavor = layananFlavor;

    this.flav = 1;

    this.setFlav = function(flav){
        this.flav = flav;
    };

    this.getFlav = function(get){
        return this.flav = get;
    };
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