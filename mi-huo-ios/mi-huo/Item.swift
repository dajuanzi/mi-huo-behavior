//
//  Item.swift
//  mi-huo
//
//  Created by Daniella Zhou on 2025-01-26.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
