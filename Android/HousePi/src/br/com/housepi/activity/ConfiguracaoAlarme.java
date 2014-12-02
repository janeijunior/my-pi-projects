package br.com.housepi.activity;

import java.io.Reader;
import java.io.StringReader;

import org.jdom2.Attribute;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class ConfiguracaoAlarme extends Fragment implements OnClickListener {
	private Button btnSalvar;
	private CheckBox cbxUsarSirene;
	private CheckBox cbxUsarEmail;
	private CheckBox cbxDesligar;
	private CheckBox cbxSensor0;
	private CheckBox cbxSensor1;
	private CheckBox cbxSensor2;
	private CheckBox cbxSensor3;
	private CheckBox cbxSensor4;
	private CheckBox cbxSensor5;
	private CheckBox cbxSensor6;
	private CheckBox cbxSensor7;
	private EditText edtTempoDisparo;
	private EditText edtNomeSensor0;
	private EditText edtNomeSensor1;
	private EditText edtNomeSensor2;
	private EditText edtNomeSensor3;
	private EditText edtNomeSensor4;
	private EditText edtNomeSensor5;
	private EditText edtNomeSensor6;
	private EditText edtNomeSensor7;	
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		
		View rootView = inflater.inflate(R.layout.configuracao_alarme, container, false);

		btnSalvar = (Button) rootView.findViewById(R.id.btnSalvarConfAlarme);
		btnSalvar.setOnClickListener(this);
		
		cbxUsarEmail = (CheckBox) rootView.findViewById(R.id.cbxUsarEmail);
		cbxUsarSirene = (CheckBox) rootView.findViewById(R.id.cbxUsarSirene);
		cbxDesligar = (CheckBox) rootView.findViewById(R.id.cbxDesligar);
		cbxSensor0 = (CheckBox) rootView.findViewById(R.id.cbxSensor0);
		cbxSensor1 = (CheckBox) rootView.findViewById(R.id.cbxSensor1);
		cbxSensor2 = (CheckBox) rootView.findViewById(R.id.cbxSensor2);
		cbxSensor3 = (CheckBox) rootView.findViewById(R.id.cbxSensor3);
		cbxSensor4 = (CheckBox) rootView.findViewById(R.id.cbxSensor4);
		cbxSensor5 = (CheckBox) rootView.findViewById(R.id.cbxSensor5);
		cbxSensor6 = (CheckBox) rootView.findViewById(R.id.cbxSensor6);
		cbxSensor7 = (CheckBox) rootView.findViewById(R.id.cbxSensor7);
		
		edtTempoDisparo = (EditText) rootView.findViewById(R.id.edtTempoDisparo);
		edtNomeSensor0 = (EditText) rootView.findViewById(R.id.edtNomeSensor0);
		edtNomeSensor1 = (EditText) rootView.findViewById(R.id.edtNomeSensor1);
		edtNomeSensor2 = (EditText) rootView.findViewById(R.id.edtNomeSensor2);
		edtNomeSensor3 = (EditText) rootView.findViewById(R.id.edtNomeSensor3);
		edtNomeSensor4 = (EditText) rootView.findViewById(R.id.edtNomeSensor4);
		edtNomeSensor5 = (EditText) rootView.findViewById(R.id.edtNomeSensor5);
		edtNomeSensor6 = (EditText) rootView.findViewById(R.id.edtNomeSensor6);
		edtNomeSensor7 = (EditText) rootView.findViewById(R.id.edtNomeSensor7);
		
		getConfiguracaoAtual();
		
		return rootView;
	}
	
	@Override
	public void onClick(View v) {
		if (v == btnSalvar) {
			if (edtTempoDisparo.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe o tempo de disparo do alarme.", this.getActivity());
			} else if (edtNomeSensor0.getText().toString().trim().equals("") || edtNomeSensor1.getText().toString().trim().equals("") ||
					   edtNomeSensor2.getText().toString().trim().equals("") || edtNomeSensor3.getText().toString().trim().equals("") ||
				       edtNomeSensor4.getText().toString().trim().equals("") || edtNomeSensor5.getText().toString().trim().equals("") ||
					   edtNomeSensor6.getText().toString().trim().equals("") || edtNomeSensor7.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe o nome de todos os sensores antes de salvar.", this.getActivity());
			} else {
				String mensagem = "";
				
				Document doc = new Document();
				Element root = new Element("AlterarConfiguracaoAlarme");
				         
				root.addContent(new Element("TempoDisparo").setText(edtTempoDisparo.getText().toString()));
				root.addContent(new Element("UsarEmail").setText(cbxUsarEmail.isChecked()?"1":"0"));
				root.addContent(new Element("UsarSirene").setText(cbxUsarSirene.isChecked()?"1":"0"));
				
				try {
					root.addContent(new Element("DesligarDisparoConsecutivo").setText(cbxDesligar.isChecked()?"1":"0"));
				} catch (Exception e) {
					e.printStackTrace();
				}
					
				Element sensor;
				Element sensores = new Element("Sensores");
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "0"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor0.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor0.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "1"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor1.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor1.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "2"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor2.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor2.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "3"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor3.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor3.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "4"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor4.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor4.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "5"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor5.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor5.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "6"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor6.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor6.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				sensor = new Element("Sensor");
				sensor.setAttribute(new Attribute("Id", "7"));
				sensor.setAttribute(new Attribute("Nome", edtNomeSensor7.getText().toString()));
				sensor.setAttribute(new Attribute("Ativo", cbxSensor7.isChecked()?"1":"0"));
				sensores.addContent(sensor);
				
				root.addContent(sensores);
				doc.setRootElement(root);
				
				mensagem = new XMLOutputter().outputString(doc);				
				Conexao.getConexaoAtual().enviarMensagem(mensagem);
					
				mensagem = Conexao.getConexaoAtual().receberRetorno();
				
				if (mensagem.equals("Ok")) {
					Funcoes.msgToastDadosGravados(this.getActivity());
				} else {
					Funcoes.msgToastErroGravar(this.getActivity());
				}
			}
		}		
	}
	
	private void getConfiguracaoAtual() {
		try {		
			Document doc = new Document();
			Element root = new Element("EnviarConfiguracaoAlarme");
			doc.setRootElement(root);
	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	
			String mensagem = "";
	
			mensagem = Conexao.getConexaoAtual().receberRetorno();
	
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);
	
			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}
	
			Element retorno = (Element) doc.getRootElement();
			
			if (!retorno.getName().equals("EnviarConfiguracaoAlarme")) {
				Funcoes.msgToastErroComando(this.getActivity());
				return;
			}
			
			cbxUsarSirene.setChecked(retorno.getChild("Geral").getAttribute("UsarSirene").getIntValue() == 1);
			cbxUsarEmail.setChecked(retorno.getChild("Geral").getAttribute("UsarEmail").getIntValue() == 1);
			
			try {
				cbxDesligar.setChecked(retorno.getChild("Geral").getAttribute("DesligarDisparoConsecutivo").getIntValue() == 1);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			edtTempoDisparo.setText(retorno.getChild("Geral").getAttribute("TempoDisparo").getValue());
			
			Element sensores = retorno.getChild("Sensores");
			
			edtNomeSensor0.setText(sensores.getChild("Sensor0").getAttribute("Nome").getValue());
			edtNomeSensor1.setText(sensores.getChild("Sensor1").getAttribute("Nome").getValue());
			edtNomeSensor2.setText(sensores.getChild("Sensor2").getAttribute("Nome").getValue());
			edtNomeSensor3.setText(sensores.getChild("Sensor3").getAttribute("Nome").getValue());
			edtNomeSensor4.setText(sensores.getChild("Sensor4").getAttribute("Nome").getValue());
			edtNomeSensor5.setText(sensores.getChild("Sensor5").getAttribute("Nome").getValue());
			edtNomeSensor6.setText(sensores.getChild("Sensor6").getAttribute("Nome").getValue());
			edtNomeSensor7.setText(sensores.getChild("Sensor7").getAttribute("Nome").getValue());
			
			cbxSensor0.setChecked(sensores.getChild("Sensor0").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor1.setChecked(sensores.getChild("Sensor1").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor2.setChecked(sensores.getChild("Sensor2").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor3.setChecked(sensores.getChild("Sensor3").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor4.setChecked(sensores.getChild("Sensor4").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor5.setChecked(sensores.getChild("Sensor5").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor6.setChecked(sensores.getChild("Sensor6").getAttribute("Ativo").getIntValue() == 1);
			cbxSensor7.setChecked(sensores.getChild("Sensor7").getAttribute("Ativo").getIntValue() == 1);
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
