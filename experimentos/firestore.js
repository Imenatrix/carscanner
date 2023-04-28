import { initializeApp } from "firebase/app"
import { getFirestore, addDoc, collection } from 'firebase/firestore'
import csv from 'csvtojson'

const firebaseConfig = {
  apiKey: "AIzaSyAaXjja908Z3CiDgJ6Gh2vzg-LWRILqk1Q",
  authDomain: "carscanner-test.firebaseapp.com",
  projectId: "carscanner-test",
  storageBucket: "carscanner-test.appspot.com",
  messagingSenderId: "645531098789",
  appId: "1:645531098789:web:a3d303c0c4f8a69f46774c"
}

const app = initializeApp(firebaseConfig)
const db = getFirestore()

const data = await csv({}).fromFile('sample.csv')
for (let anuncio of data) {
    delete anuncio['field1']
    await addDoc(collection(db, 'anuncios'), anuncio)
}