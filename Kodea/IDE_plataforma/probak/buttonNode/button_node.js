const xml2js = require('xml2js');
const builder = new xml2js.Builder();
const fs = require('fs');

module.exports = function(RED) {
    function ButtonNode(config) {
        RED.nodes.createNode(this, config);
        
        this.function = config.function;
        var node = this;


        if (this.clickeado) {
            var RED2 = require.main.require('node-red');
            var miflow = RED2.nodes.getFlow(this.z);    // this.z -> nodoa dagoen fluxuaren IDa
            var appName = miflow.label;

            var msg = {
                payload: "mensaje",
                application_name: appName
            }
            node.send(msg);
        }

        // Handle the button configuration event
        node.on('close', function () {
            // Reset the button attribute to false when the node is closed
            config.button = false;
        });

        // Handle the button click event
        node.on('click', function() {
            var msg = {
                payload: config.button
            };
            node.send(msg);
        });

    }

    RED.nodes.registerType("Button node",ButtonNode);
}
