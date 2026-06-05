class IcfesSkill < Formula
  desc "Skill para crear, revisar y exportar items estilo ICFES"
  homepage "https://github.com/nestorfernando3/icfes-skill"
  url "https://github.com/nestorfernando3/icfes-skill/archive/refs/tags/v0.1.2.tar.gz"
  version "0.1.2"
  sha256 "d6e0b0c368500c532459931e61b1e9dfaab91c5fe5ae5d79463a6f93380edac8"
  license "MIT"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/icfes-skill" => "icfes-skill"
  end

  def caveats
    <<~EOS
      Instalar skill:
        icfes-skill install

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
