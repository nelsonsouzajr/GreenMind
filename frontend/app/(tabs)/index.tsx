import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, StatusBar } from 'react-native';
import { Link } from 'expo-router'; // 1. IMPORTAR O LINK

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      <View style={styles.logoPlaceholder}>
        <Text style={styles.logoText}>[Logo]</Text>
      </View>

      <Text style={styles.title}>GreenMind</Text>
      
      <Text style={styles.subtitle}>
        Suas plantas pedem ajuda. Vamos descobrir o que elas têm?
      </Text>

      {/* 2. USAR O LINK PARA NAVEGAR PARA A NOVA TELA 'CAPTURE' */}
      <Link href="/capture" asChild>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>ANALISAR PLANTA</Text>
        </TouchableOpacity>
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  // ... (mantenha os mesmos estilos de antes)
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  logoPlaceholder: {
    width: 100,
    height: 100,
    backgroundColor: '#e0e0e0',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  logoText: {
    color: '#a0a0a0',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2e7d32',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#616161',
    textAlign: 'center',
    marginBottom: 40,
  },
  button: {
    backgroundColor: '#4caf50',
    paddingVertical: 15,
    paddingHorizontal: 60,
    borderRadius: 30,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});