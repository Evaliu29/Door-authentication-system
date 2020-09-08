window.onload=function(){
	
	var bucket = getUrlParam("bucket")
	var objectKey = getUrlParam("key")
	var url = "https://" + bucket + ".s3.amazonaws.com/" + objectKey
	document.getElementById("unknownFace").src=url;
}

function getUrlParam(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}
function validateForm() {
    var x = document.forms["myForm"]["Visitor"].value;
	var y = document.forms["myForm"]["Phone"].value;
	var z = 
	console.log(x,y)
    if (x == "") {
        alert("please input your name");
		return false;
	}
	if (y == "") {
        alert("please input your phone number");
        return false;
    }
	if(!y.match("[0-9]{10}")){
        alert("please input right phone number");
        return false;
    }
var bucket = getUrlParam("bucket")
var objectKey = getUrlParam("key")
var createdTimestamp = getUrlParam("timestamp")
   //新建client
   var apigClient = apigClientFactory.newClient();
//发送数据与接收反馈：
apigClient.messagePost(
    {}
    ,{
     name:x,
     phonenumber:y,
	 photos:[
	 {
		 bucket:bucket,
		 objectKey: objectKey,
		 createdTimestamp:createdTimestamp
	 }
	 ]
    },
    {})
.then(function(result){
      console.log(result)
      body = result.data.response
      console.log(body)
      if(body != null){
       //var body_json = JSON.parse(body)
       //console.log(body_json.content)
	   if(body=="The information has been stored successfully! Message sent."){
		    alert("Your information has been successfully added"); 
        }else{
			alert("Your information is added unsuccessfully, please try again");
		}     
      }
    }).catch( function(result){
       console.log(result)
    });


}