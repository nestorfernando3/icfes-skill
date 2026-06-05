class IcfesSkill < Formula
  desc "Skill para crear, revisar y exportar items estilo ICFES"
  homepage "https://github.com/nestorfernando3/icfes-skill"
  url "https://github.com/nestorfernando3/icfes-skill/archive/refs/tags/v0.1.6.tar.gz"
  version "0.1.6"
  sha256 "8f1dac317f8dcc5f213cd68df35f7008cee208e23e96543b044cc13e6fbf275b"
  license "MIT"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/icfes-skill" => "icfes-skill"
  end

  def caveats
    <<~EOS
      Instalar skill:
        icfes-skill install
        # brew install/reinstall solo instala CLI. Este comando abre menu TUI.

      Global Codex:
        icfes-skill install --target codex --scope user

      Por proyecto:
        icfes-skill install --target codex --scope project --project /ruta/proyecto
    EOS
  end

  test do
    system bin/"icfes-skill", "doctor"
  end
end
