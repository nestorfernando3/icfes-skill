class IcfesSkill < Formula
  desc "Skill para crear, revisar y exportar items estilo ICFES"
  homepage "https://github.com/nestorfernando3/icfes-skill"
  url "https://github.com/nestorfernando3/icfes-skill/archive/refs/tags/v0.1.4.tar.gz"
  version "0.1.4"
  sha256 "e53bb04d787cd39db99edc706c3ee2e94b1f014a3cfd74cc906fb1c5898e7d42"
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
