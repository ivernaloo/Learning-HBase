var assert = require('assert');
var hbase = require('hbase');
var client = hbase({host: 'localhost', port: 16010});


client.getTable('miui_sec:flow_order_order').getSchema(function(err, schema){
    console.log(schema);
});

