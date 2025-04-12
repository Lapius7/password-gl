from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="password-gl",
    version="1.0.2",
    packages=["password_gl"],
    install_requires=[],
    license="MIT",
    entry_points={
        "console_scripts": [
            "password-gl = password_gl.generator:main",
            "pgl = password_gl.generator:main",
        ]
    },
    author="Lapius7bot Technology Co.",
    author_email="contact-us@lapius7.com",
    description="パスワードを生成するコマンドラインツール",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/Lapius7/pip.password-gl",
        "Bug Tracker": "https://github.com/Lapius7/pip.password-gl/issues",
    },
)