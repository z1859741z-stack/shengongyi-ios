import SwiftUI
import WebKit

/// 深宫弈 · 竖屏沉浸版：WKWebView 壳，只加载本地 index.html，不联网也能玩。
/// 存档走网页 localStorage（WKWebView 文件 URL 下可用），竖屏锁定见 Info.plist。
@main
struct ShengongyiApp: App {
    var body: some Scene {
        WindowGroup {
            WebView()
                .ignoresSafeArea()
        }
    }
}

struct WebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.defaultWebpagePreferences.allowsContentJavaScript = true
        let wv = WKWebView(frame: .zero, configuration: config)
        wv.scrollView.bounces = false
        wv.isOpaque = false
        wv.backgroundColor = UIColor(red: 0.14, green: 0.09, blue: 0.03, alpha: 1)
        if let url = Bundle.main.url(forResource: "index", withExtension: "html") {
            wv.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        }
        return wv
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
