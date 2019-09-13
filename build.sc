import mill._
import mill.scalalib._

object generator extends SbtModule {
  def scalaVersion = "2.11.12"
  def ivyDeps = Agg(ivy"com.github.scopt::scopt:3.3.0")
}
