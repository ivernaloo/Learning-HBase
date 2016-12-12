var assert = require('assert');
var hbase = require('hbase');
var client = hbase({ host: 'localhost', port: 16010 });


client.table('my_table') // use table
    .create('my_column_family', function(err, success){
        this
            .row('my_row')
            .put('my_column_family:my_column', 'my value', function(err, success){
                this.get('my_column_family', function(err, cells){
                    this.exists(function(err, exists){
                        // async callback
                        console.log("****************************************************");
                        console.log(exists);
                        assert.ok(exists);
                    });
                });
            });
    });

client.version(function( error, version ){
    console.log( version );
    console.log("****************************************************");

} );


client.version_cluster( function( error, versionCluster ){
    console.log("****************************************************");
    console.log( versionCluster );
} );

client.status_cluster( function( error, statusCluster ){
    console.log("****************************************************");
    console.log( statusCluster );
} );

client.tables( function( error, tables ){
    console.log("****************************************************");
    console.log( tables );
} );