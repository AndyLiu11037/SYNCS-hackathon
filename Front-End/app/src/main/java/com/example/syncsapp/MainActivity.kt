package com.example.syncsapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import kotlinx.android.synthetic.main.activity_main.*

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
        val url = "https://australia-southeast1-syncs-hackathon.cloudfunctions.net/detect"

        val jsonObjectRequest = JsonObjectRequest(
            Request.Method.GET, url, null,
            { response ->
                textView.text = "Response: %s".format(response.toString())
            },
            { error ->
                // TODO: Handle error
            }
        )

    }
}