var assert = require('assert');
var hbase = require('hbase');
var client = hbase({ host: '192.168.99.100', port: 32776 }) 


    .table('my_table' )
    .create('my_column_family', function(err, success){
        this
            .row('my_row')
            .put('my_column_family:my_column', 'my value', function(err, success){
                this.get('my_column_family', function(err, cells){
                    this.exists(function(err, exists){
                        console.log("ok");
                        console.log(exists);
                        assert.ok(exists);
                    });
                });
            });
    });