//usr/bin/zig run "$0" -- foo bar && exit $?
const std = @import("std");

pub fn main() anyerror!void {
    std.log.info("All your codebase are belong to us.", .{});
    var general_purpose_allocator = std.heap.GeneralPurposeAllocator(.{}){};
    const gpa = general_purpose_allocator.allocator();
    const args = try std.process.argsAlloc(gpa);
    defer std.process.argsFree(gpa, args);
    for (args[1..]) |arg, i| {
       std.debug.print("{}: {s}\n", .{ i, arg });
    }
}

test "basic test" {
    try std.testing.expectEqual(10, 3 + 7);
}
