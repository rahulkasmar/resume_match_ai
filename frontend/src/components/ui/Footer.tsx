export default function Footer() {
    return (
        <footer className="bg-transparent py-8 mt-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <p className="text-center text-sm text-gray-400">
                    &copy; {new Date().getFullYear()} Resume AI. All rights reserved.
                </p>
            </div>
        </footer>
    );
}