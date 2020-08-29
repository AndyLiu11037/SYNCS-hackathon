package com.example.syncsapp


import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import android.widget.Button
import android.widget.Toast
import androidx.core.content.FileProvider
import kotlinx.android.synthetic.main.activity_camera.*
import java.io.File

private const val REQUEST_CODE = 42;
private const val FILE_NAME = "PHOTO.jpeg";
private lateinit var photoFile : File;

class CameraActivity : AppCompatActivity(){

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_camera)

        val takePicButton = findViewById<Button>(R.id.takePicture)
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
        }else{
            super.onActivityResult(requestCode, resultCode, data);
        }
    }
}