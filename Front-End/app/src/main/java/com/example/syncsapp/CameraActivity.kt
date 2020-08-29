package com.example.syncsapp


import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import android.widget.Button
import android.widget.Toast
import androidx.core.content.FileProvider
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject
import kotlinx.android.synthetic.main.activity_camera.*
import java.io.ByteArrayOutputStream
import java.io.File

private const val REQUEST_CODE = 42;
private const val FILE_NAME = "PHOTO.jpeg";
private const val URL = "https://australia-southeast1-syncs-hackathon.cloudfunctions.net/detect";
private lateinit var photoFile : File;

class CameraActivity : AppCompatActivity(){

    private var currButton : Button? = null;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_camera)

        val takePicButton = findViewById<Button>(R.id.takePicture);

        takePicButton.setOnClickListener {
            val openCameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            photoFile = getPhotoFile(FILE_NAME);

            val fileProvider = FileProvider.getUriForFile(this, "syncsapp.fileprovider", photoFile);
            openCameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, fileProvider);

            if (openCameraIntent.resolveActivity(this.packageManager) != null) {
                startActivityForResult(openCameraIntent, REQUEST_CODE);
            } else {
                Toast.makeText(this, "Unable to open camera", Toast.LENGTH_SHORT).show();
            }
        }

        val shapeClick = View.OnClickListener(){
            if(this.currButton != null){
                this.currButton!!.background.setTint(Color.parseColor("#E86A92"));
            }

            this.currButton = it as Button;
            this.currButton!!.background.setTint(Color.parseColor("#41E2BA"));
        }

        circleButton.setOnClickListener(shapeClick);
        parallelButton.setOnClickListener(shapeClick);
        rectangleButton.setOnClickListener(shapeClick);
    }

    private fun getPhotoFile(fileName: String): File {
        val storageDirectory = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        return File.createTempFile(fileName,".jpg", storageDirectory);
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if(requestCode == REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            val takenImage = BitmapFactory.decodeFile(photoFile.absolutePath);
            imageView.setImageBitmap(takenImage);
            imageView.visibility = View.VISIBLE;

            var baos = ByteArrayOutputStream();
            takenImage.compress(Bitmap.CompressFormat.JPEG, 100, baos);
            val encodedImage = Base64.encodeToString(baos.toByteArray(), Base64.DEFAULT);

            val pictureObj = JSONObject();
            pictureObj.put("image", encodedImage);
            pictureObj.put( "shape", this.currButton!!.text);

            val request = JsonObjectRequest(
                Request.Method.POST,
                URL,
                pictureObj,
                Response.Listener<JSONObject> {
                    response ->
                    Log.d("CAMERA", "Response object is ${response.toString()}")

//                    val imageBytes = Base64.decode(response.get("image") as String, Base64.DEFAULT);
//                    val decodedImage = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.size);
//                    imageView.setImageBitmap(decodedImage);

                    dispatchScoreIntent(response.get("image") as String, response.get("score") as String);
                },
                Response.ErrorListener{
                    error ->
                    Log.d("CAMERA","error: ${error.message}")
                }
            )

            val queue = Volley.newRequestQueue(this);
            queue.add(request);

        }else{
            super.onActivityResult(requestCode, resultCode, data);
        }
    }

    private fun dispatchScoreIntent(base64Image: String, score: String) {
        val intent = Intent(this, ScoreActivity::class.java);
        intent.putExtra("image", base64Image);
        intent.putExtra("score", score);
        startActivity(intent);
    }
}