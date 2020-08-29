package com.example.syncsapp

import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.widget.TextView
import kotlinx.android.synthetic.main.activity_camera.*
import kotlinx.android.synthetic.main.activity_score.*

class ScoreActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_score)

        val parsedIntent = intent;

        val b64Img = parsedIntent.getStringExtra("image");
        val percent = parsedIntent.getStringExtra("score");

        val imageBytes = Base64.decode(b64Img, Base64.DEFAULT);
        val decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size);

        picture.setImageBitmap(decodedImage);
        val percentTextView = findViewById<TextView>(R.id.percent);
        percentTextView.text = percent;

    }
}