package com.example.syncsapp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button

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
            openLeaderboardIntent();
        }
    }

    fun openLeaderboardIntent() {
        val intent = Intent(this, LeaderboardActivity::class.java);
        startActivity(intent);
    }

    fun openCameraActivityIntent() {
        
    }

}