import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, StatusBar, Image } from 'react-native';
import { Link } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient'; // Importamos o componente de gradiente

export default function HomeScreen() {
  return (
    // Usamos o LinearGradient como o contentor principal
    <LinearGradient
      colors={['#f5f5f5', '#e8f5e9', '#c8e6c9']} // Gradiente suave de cinza claro para verde
      style={styles.container}
    >
      <StatusBar barStyle="dark-content" />
      
      <Image 
        source={require('../../assets/images/Logo.png')} 
        style={styles.logo}
        resizeMode="contain"
      />

      <Text style={styles.title}>GreenMind</Text>
      
      <Text style={styles.subtitle}>
        O seu assistente pessoal para um jardim mais saudável.
      </Text>

      <Link href="/capture" asChild>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>ANALISAR PLANTA</Text>
        </TouchableOpacity>
      </Link>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  logo: {
    width: 150,
    height: 150,
    marginBottom: 20,
  },
  title: {
    fontSize: 48, // Aumentamos o tamanho para mais impacto
    fontWeight: 'bold',
    color: '#1b5e20', // Um tom de verde mais escuro e sóbrio
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    color: '#388e3c', // Um verde médio para o subtítulo
    textAlign: 'center',
    marginBottom: 60, // Aumentamos o espaçamento
    paddingHorizontal: 20,
  },
  button: {
    backgroundColor: '#4caf50',
    paddingVertical: 18, // Ligeiramente maior
    paddingHorizontal: 80,
    borderRadius: 50, // Mais arredondado
    // Adicionamos uma sombra para dar profundidade
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});