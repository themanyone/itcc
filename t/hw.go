//home/k/bin/runner go build "$0" -- foo bar && exit 0
package main; import ("fmt"; "os")
func main() { fmt.Printf("Args 1: %s\n", os.Args[1]) }
