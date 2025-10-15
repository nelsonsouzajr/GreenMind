import { Text, View, StyleSheet } from 'react-native';

export default function MeuJardimScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Meu Jardim</Text>
      <Text>Aqui ficará o histórico das suas plantas.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
});