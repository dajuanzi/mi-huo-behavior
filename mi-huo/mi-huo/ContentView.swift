//
//  ContentView.swift
//  mi-huo
//
//  Created by Daniella Zhou on 2025-01-26.
//

import SwiftUI

struct ContentView: View {
    @State private var theme = "职场"
    @State private var level: Double = 3
    @State private var result = "迷惑行为会出现在这里"

    var body: some View {
        VStack(spacing: 20) {
            Text("迷惑行为生成器")
                .font(.largeTitle)
                .bold()

            Picker("选择主题", selection: $theme) {
                Text("职场").tag("职场")
                Text("校园").tag("校园")
                Text("家庭").tag("家庭")
            }
            .pickerStyle(SegmentedPickerStyle())

            Slider(value: $level, in: 1...5, step: 1) {
                Text("迷惑程度")
            }
            Text("迷惑程度：\(Int(level))")

            Button("生成迷惑行为") {
                // 调用生成函数
                result = "生成中..."
                generateConfusion(theme: theme, level: Int(level)) { generatedText in
                    result = generatedText
                }
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)

            Text(result)
                .padding()
                .multilineTextAlignment(.center)
        }
        .padding()
    }

    func generateConfusion(theme: String, level: Int, completion: @escaping (String) -> Void) {
        // Construct the URL with query parameters
        var urlComponents = URLComponents(string: "http://127.0.0.1:8000/generate_confusion/")!
        urlComponents.queryItems = [
            URLQueryItem(name: "theme", value: theme),
            //URLQueryItem(name: "level", value: "\(level)")
        ]
        
        guard let url = urlComponents.url else {
            completion("生成失败：URL无效")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Since the curl example does not include a body, remove any body-related code
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    completion("生成失败：\(error.localizedDescription)")
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    completion("生成失败：无响应数据")
                }
                return
            }
            
            do {
                if let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                   let confusion = jsonResponse["confusion"] as? String {
                    DispatchQueue.main.async {
                        completion(confusion)
                    }
                } else {
                    DispatchQueue.main.async {
                        completion("生成失败：响应格式无效")
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    completion("生成失败：JSON解析错误")
                }
            }
        }.resume()
    }
}


#Preview {
    ContentView()
        .modelContainer(for: Item.self, inMemory: true)
}
