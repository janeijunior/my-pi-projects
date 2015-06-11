package br.com.housepi.classes;
import java.io.Reader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import android.view.View;
import android.widget.ToggleButton;
import br.com.housepi.classes.Conexao;

public class Rele {
	private Integer status;
	private Integer numero;
	private String nome;
	private Integer ativo;
	private ToggleButton botao;
	private static List<String> nomeReles = new ArrayList<String>();
	private Integer temporizador;
	
	public Rele(Integer numero, ToggleButton botao) {
		super();
		this.numero = numero;
		this.botao = botao;
	}

	public Rele(Integer numero) {
		super();
		this.numero = numero;
	}

	public Integer getStatus() {
	    
		return status;
	}

	public ToggleButton getBotao() {
		return botao;
	}

	public void setBotao(ToggleButton botao) {
		this.botao = botao;
	}

	public void setStatus(Integer status) {
		this.status = status;
	}

	public Integer getNumero() {
		return numero;
	}

	public void setNumero(Integer numero) {
		this.numero = numero;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}	
	
	public Integer getAtivo() {
		return ativo;
	}

	public void setAtivo(Integer ativo) {
		this.ativo = ativo;
	}
	
	public Integer getTemporizador() {
		return temporizador;
	}

	public void setTemporizador(Integer temporizador) {
		this.temporizador = temporizador;
	}

	public Boolean ligar() {
		return montarEnviarXMLControle("Ligar");
	}
	
	public Boolean desligar() {
		return montarEnviarXMLControle("Desligar");
	}
	
	private Boolean montarEnviarXMLControle(String comando) {
		Document doc = new Document();
		Element root = new Element("Rele");
		       
		Element acao = new Element("Acao");
		acao.setText(comando);
		root.addContent(acao);
		
		Element numero = new Element("Numero");
		numero.setText(getNumero().toString());
		root.addContent(numero);
		
		Element temporizador = new Element("Temporizador");
		temporizador.setText(getTemporizador().toString());
		root.addContent(temporizador);
		
		doc.setRootElement(root);
		
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		if (Conexao.receberRetornoStatic().equals("Ok")) {
			return true;
		} else {
			return false;
		}
	}
	
	public static List<Rele> getConfiguracaoStatus(List<Rele> listaReles) {
		try {
			Document doc = new Document();
			Element root = new Element("StatusRele");
			doc.setRootElement(root);

			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

			String mensagem = "";

			mensagem = Conexao.receberRetornoStatic();
						
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);

			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}

			Element retorno = (Element) doc.getRootElement();
			
			if (!retorno.getName().equals("StatusRele")) {
				return listaReles;
			}
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();

			if (j.hasNext()) {
				nomeReles.clear();
			}
			
			for (Rele rele : listaReles) {
				Element element = (Element) j.next();
		
				rele.setStatus(element.getAttribute("Status").getIntValue());
				rele.setNome(element.getAttribute("Nome").getValue());
				rele.setAtivo(element.getAttribute("Ativo").getIntValue());
				
				nomeReles.add(rele.getNome());
				
				if (rele.getBotao() != null) {
					rele.getBotao().setChecked(rele.getStatus() == 1);
					rele.getBotao().setText(rele.getNome());
					rele.getBotao().setTextOn(rele.getNome());
					rele.getBotao().setTextOff(rele.getNome());
				
					if (rele.getAtivo() == 1) {
						rele.getBotao().setVisibility(View.VISIBLE);
					} else {
						rele.getBotao().setVisibility(View.GONE);
					}
				}
			}
		
		return listaReles;
		
		} catch (Exception e) {
			for (int i = 0; i < 10; i++) {
				if (listaReles.get(i).getBotao() != null) {
					listaReles.get(i).getBotao().setText(nomeReles.get(i));
					listaReles.get(i).getBotao().setTextOn(nomeReles.get(i));
					listaReles.get(i).getBotao().setTextOff(nomeReles.get(i));
					listaReles.get(i).getBotao().setVisibility(View.VISIBLE);
				}
			}
			
			return listaReles;
		}
	}
}
