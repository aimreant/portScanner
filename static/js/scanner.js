/**
 * Created by aimreant on 5/17/16.
 */
$(document).ready(function(){
    var ani_time = 300;

    $("#single_tab").click(function(){
        $("#single_port").show(ani_time);
        $("#multi_port").hide(ani_time);
        $("#common_port").hide(ani_time);
        $("#multi_ip").hide(ani_time);
        $("#single_tab").addClass("active");
        $("#multi_tab").removeClass("active");
        $("#common_tab").removeClass("active");
        $("#multi_ip_tab").removeClass("active");
    });
    $("#multi_tab").click(function(){
        $("#single_port").hide(ani_time);
        $("#multi_port").show(ani_time);
        $("#common_port").hide(ani_time);
        $("#multi_ip").hide(ani_time);
        $("#single_tab").removeClass("active");
        $("#multi_tab").addClass("active");
        $("#common_tab").removeClass("active");
        $("#multi_ip_tab").removeClass("active");
    });
    $("#multi_ip_tab").click(function(){
        $("#single_port").hide(ani_time);
        $("#multi_port").hide(ani_time);
        $("#common_port").hide(ani_time);
        $("#multi_ip").show(ani_time);
        $("#single_tab").removeClass("active");
        $("#multi_tab").removeClass("active");
        $("#multi_ip_tab").addClass("active");
        $("#common_tab").removeClass("active");
    });
    $("#common_tab").click(function(){
        $("#single_port").hide(ani_time);
        $("#multi_port").hide(ani_time);
        $("#common_port").show(ani_time);
        $("#multi_ip").hide(ani_time);
        $("#single_tab").removeClass("active");
        $("#multi_tab").removeClass("active");
        $("#common_tab").addClass("active");
        $("#multi_ip_tab").removeClass("active");
    });


    $("#single_scan").click(function(){
        $("#output").html("Waiting..");
        $.post("/ip_port/",
            {
                method: "selected",
                ip: $("#sin_ip").val(),
                port: $("#sin_port").val(),
            },
            function(json){
                var output_html = "<table class='table'><tbody><thead><tr><th>IP</th><th>端口</th><th>服务</th><th>描述</th> </tr> </thead>";
                for(var i=0;i<json['open_ports_msg'].length;i++){
                    output_html = output_html + "<tr>" +json['open_ports_msg'][i] + "</tr>";
                }
                output_html = output_html + "</tbody></table>";
                $("#output").html(output_html);
            }
        );
    });

    $("#multi_scan").click(function(){
        $("#output").html("Waiting..");
        $.post("/ip_port/",
            {
                method: "sequential",
                ip: $("#mul_ip").val(),
                start_port: $("#start_port").val(),
                end_port: $("#end_port").val(),
            },
            function(json){
                var output_html = "<table class='table'><tbody><thead><tr><th>IP</th><th>端口</th><th>服务</th><th>描述</th> </tr> </thead>";
                for(var i=0;i<json['open_ports_msg'].length;i++){
                    output_html = output_html + "<tr>" +json['open_ports_msg'][i] + "</tr>";
                }
                output_html = output_html + "</tbody></table>";
                $("#output").html(output_html);
            }
        );
    });

    $("#multi_ip_scan").click(function(){
        $("#output").html("Waiting..");
        $.post("/ip_port/",
            {
                method: "multi_ip",
                ip: 'localhost',
                start_ip: $("#start_ip").val(),
                end_ip: $("#end_ip").val(),
                multi_ip_start_port: $("#multi_ip_start_port").val(),
                multi_ip_end_port: $("#multi_ip_end_port").val(),
            },
            function(json){
                var output_html = "<table class='table'><tbody><thead><tr><th>IP</th><th>端口</th><th>服务</th><th>描述</th> </tr> </thead>";
                for(var i=0;i<json['open_ports_msg'].length;i++){
                    output_html = output_html + "<tr>" +json['open_ports_msg'][i] + "</tr>";
                }
                output_html = output_html + "</tbody></table>";
                $("#output").html(output_html);
            }
        );
    });

    $("#common_scan").click(function(){
        $("#output").html("Waiting..");
        $.post("/ip_port/",
            {
                method: "common",
                ip: $("#com_ip").val(),
            },
            function(json){
                var output_html = "<table class='table'><tbody><thead><tr><th>IP</th><th>端口</th><th>服务</th><th>描述</th> </tr> </thead>";
                for(var i=0;i<json['open_ports_msg'].length;i++){
                    output_html = output_html + "<tr>" +json['open_ports_msg'][i] + "</tr>";
                }
                output_html = output_html + "</tbody></table>";
                $("#output").html(output_html);
            }
        );
    });
});