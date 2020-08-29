package com.example.syncsapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonArrayRequest
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        val playButton = findViewById<Button>(R.id.playButton);
        playButton.setOnClickListener{
            Log.d("BUTTON", "The playbutton is being clicked");
        }

        val leaderboardButton = findViewById<Button>(R.id.leaderboardButton);
        leaderboardButton.setOnClickListener{
            openLeaderboard();
        }
    }

    fun openLeaderboard() {
        //val intent = Intent(this, LeaderboardActivity::class.java);
        //startActivity(intent);
        val queue = Volley.newRequestQueue(this)
    //https://australia-southeast1-syncs-hackathon.cloudfunctions.net/detect
        val url = "https://www.google.com/"
        val textView = findViewById<TextView>(R.id.textView)
        val stringRequest = StringRequest(Request.Method.GET, url,
            { response ->
                textView.text = "Response is: ${response.substring(0,500)}"
            },
            { textView.text = "Bad" })

       /*val jsonObjectRequest = JsonArrayRequest(
            Request.Method.GET, url, null,
            Response.Listener { response ->

                textView.text = "Response: %s".format(response.toString())
            },
            Response.ErrorListener{ error ->
                // TODO: Handle error
                val textView = findViewById<TextView>(R.id.textView)
                textView.text = "Bad"
            }
        )
        */

        queue.add(stringRequest)

    }
}