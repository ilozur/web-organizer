using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Text;
using System.IO;

public class Controller : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    string get_csrf()
    {
        var httpRequest = (HttpWebRequest)WebRequest.Create("http://127.0.0.1:8000/api/get_csrf");
        httpRequest.Method = "GET";
        httpRequest.ContentType = "application/json";
        using (var httpResponse = httpRequest.GetResponse())
        using (var responseStream = httpResponse.GetResponseStream())
        using (var reader = new StreamReader(responseStream))
        {
            string response = reader.ReadToEnd();
            return response;
        }
    }
}
