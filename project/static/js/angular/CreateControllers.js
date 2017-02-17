var app = angular.module('CreateControllers', []);

app.controller('CreateinstanceController', function () {
    this.createInstance = [
        {
            name: "ubuntu",
            image_logo: "/static/img/ubuntu.jpg",
            version: 1
        },
        {
            name: "debian",
            image_logo: "/static/img/debian.jpg",
            version: 1
        },
        {
            name: "centOS",
            image_logo: "/static/img/centOS.jpg",
            version: 1
        },
        {
            name: "fedora",
            image_logo: "/static/img/fedora.jpg",
            version: 1
        }
    ];


});

app.controller('CreateappsController', function () {
    this.createApps = apps;
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

app.controller('CreateflavorController', function () {
    this.cFlavor = [
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

app.controller('CreatecustomflavorController', function () {
    
});