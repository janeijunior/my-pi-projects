package br.com.housepi.classes;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class Banco extends SQLiteOpenHelper {
	
	private static final String DATABASE_NAME = "HousePi";
	private static final int DATABASE_VERSION = 2;
	
	public Banco(Context context) {	
		super(context, DATABASE_NAME, null, DATABASE_VERSION);
	}
	
	@Override
	public void onCreate(SQLiteDatabase db) {
		String sql = "create table Conexao (Id integer primary key autoincrement,  Descricao text, Host text, Porta text, ConectarAutomaticamente int)";
		db.execSQL(sql);
	}

	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		
		
	}
}
