function validateForm() {
    var msg = document.forms["myForm"]["opt"].value;
    if (msg == "") {
        alert("Please input your OTP");
		return false;
    }
	
	//新建client
    var apigClient = apigClientFactory.newClient();
    //发送数据与接收反馈：
    apigClient.oTPPost(
    {}
    ,{
     OTP:msg
    },
    {})
    .then(function(result){
    console.log(result)
    body = result.data.body
    console.log(body)
	if(body != null){
       var body_json = JSON.parse(body)
       console.log(body_json.content)
	   if(body_json=="Wrong OTP"){
		    alert("permission denied"); 
	   }else{
		    alert("Hello, "+body_json+". The virtual door has been opened successfully!")
	   } 
	}  
    }).catch( function(result){
       console.log(result)
    });
}