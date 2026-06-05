class IcfesSkill < Formula
  desc "Skill para crear, revisar y exportar items estilo ICFES"
  homepage "https://github.com/nestorfernando3/icfes-skill"
  url "https://github.com/nestorfernando3/icfes-skill/archive/refs/tags/v0.1.15.tar.gz"
  version "0.1.15"
  sha256 "5994de9e7c7d09f904bc9734c77799729e1f494cf5acf59dcaa79cd347e8c2ae"
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
