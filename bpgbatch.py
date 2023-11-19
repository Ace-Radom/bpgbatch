import os
import shutil
import sys
import unicodedata

def replace_unicode_chars( filename ) -> str:
    directory, old_filename = os.path.split( filename )
    base_name, extension = os.path.splitext( old_filename )
    filesystem_encoding = sys.getfilesystemencoding()
    normalized_base_name = unicodedata.normalize( 'NFKD' , base_name ).encode( filesystem_encoding , 'ignore' ).decode( filesystem_encoding )
    normalized_base_name = ''.join( c if c.isalnum() else '-' for c in normalized_base_name )
    new_filename = f"copy-{normalized_base_name}{extension}"
    new_filepath = os.path.join( directory , new_filename )
    return new_filepath

def get_all_bpg_files( dir: str ) -> list[str]:
    filelist = []
    for root , ds , fs in os.walk( dir ):
        for f in fs:
            if f.endswith( ".bpg" ):
                fullname = os.path.join( root , f )
                filelist.append( fullname )
    return filelist

def main():
    if len( sys.argv ) == 1:
        print( "Please input the target directory" )
        exit( 1 )

    target_dir = sys.argv[1]
    if not os.path.exists( target_dir ):
        print( "Illegal input: target directory doesn't exist" )
        exit( 1 )
    if not os.path.isdir( target_dir ):
        print( "Illegal input: target directory is not a directory" )
        exit( 1 )
    
    bpg_files = get_all_bpg_files( target_dir )
    print( "Found" , len( bpg_files ) , "in total" )
    if not os.path.exists( "./output" ):
        os.mkdir( "output" )
    for file in bpg_files:
        cmd = "bpgdec.exe -o ./output/" + os.path.basename( file ) + ".png " + file
        print( "Running command: \"" , cmd , "\"" , sep = "" )
        ret = os.system( cmd )
        if ret != 0:
            print( "Failed, replace unicode chars and retry..." )
            new_filepath_after_replace = replace_unicode_chars( file )
            try:
                shutil.copy2( file , new_filepath_after_replace )
                print( "Create a copy of original file \"" , file , "\": \"" , new_filepath_after_replace , "\"" , sep = "" )
                cmd = "bpgdec.exe -o ./output/" + os.path.basename( new_filepath_after_replace ) + ".png " + new_filepath_after_replace
                print( "Running command: \"" , cmd , "\"" , sep = "" )
                ret = os.system( cmd )
                if ret == 0:
                    print( "Success" )
                else:
                    print( "Failed" )
            except OSError as e:
                print( "OSError:" , e )
            except Exception as e:
                print( "Unknown Error:" , e )
        else:
            print( "Success" )
    
if __name__ == "__main__":
    main()
