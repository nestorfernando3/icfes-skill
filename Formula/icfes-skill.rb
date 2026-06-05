class IcfesSkill < Formula
  desc "Skill para crear, revisar y exportar items estilo ICFES"
  homepage "https://github.com/nestorfernando3/icfes-skill"
  url "https://github.com/nestorfernando3/icfes-skill/archive/refs/tags/v0.1.10.tar.gz"
  version "0.1.10"
  sha256 "f1bea130c50c646194b70301ae0dcdb5de74bb1a43eba8a2fa62acc24d7e360b"
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
