//
//  ContentView.swift
//  Weather
//
//  Created by Mirko Kopsa on 19.12.2024.
//

import SwiftUI
import WebKit

struct WebView: UIViewRepresentable {

    func makeUIView(context: UIViewRepresentableContext<WebView>) -> WebView.UIViewType {
        WKWebView(frame: .zero)
    }

    func updateUIView(_ uiView: WKWebView, context: UIViewRepresentableContext<WebView>) {
        let request = URLRequest(url: URL(string: "http://34.88.17.114:3000/public-dashboards/065a88665edf45b08eb5a912ab36a494")!)
        uiView.load(request)
    }

}

struct ContentView: View {
    var body: some View {
        WebView()
    }
}

#Preview {
    ContentView()
}
